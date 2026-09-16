// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature05Data",
    products: [.library(name: "Feature05Data", targets: ["Feature05Data"])],
    dependencies: [.package(path: "../Feature05Domain")],
    targets: [.target(name: "Feature05Data", dependencies: [.product(name: "Feature05Domain", package: "Feature05Domain")])]
)
