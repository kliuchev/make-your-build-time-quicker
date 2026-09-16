// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature09Data",
    products: [.library(name: "Feature09Data", targets: ["Feature09Data"])],
    dependencies: [.package(path: "../Feature09Domain")],
    targets: [.target(name: "Feature09Data", dependencies: [.product(name: "Feature09Domain", package: "Feature09Domain")])]
)
