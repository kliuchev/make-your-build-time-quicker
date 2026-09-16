// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature26Data",
    products: [.library(name: "Feature26Data", targets: ["Feature26Data"])],
    dependencies: [.package(path: "../Feature26Domain")],
    targets: [.target(name: "Feature26Data", dependencies: [.product(name: "Feature26Domain", package: "Feature26Domain")])]
)
