// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature20Data",
    products: [.library(name: "Feature20Data", targets: ["Feature20Data"])],
    dependencies: [.package(path: "../Feature20Domain")],
    targets: [.target(name: "Feature20Data", dependencies: [.product(name: "Feature20Domain", package: "Feature20Domain")])]
)
