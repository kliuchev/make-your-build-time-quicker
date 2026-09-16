// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature29Data",
    products: [.library(name: "Feature29Data", targets: ["Feature29Data"])],
    dependencies: [.package(path: "../Feature29Domain")],
    targets: [.target(name: "Feature29Data", dependencies: [.product(name: "Feature29Domain", package: "Feature29Domain")])]
)
